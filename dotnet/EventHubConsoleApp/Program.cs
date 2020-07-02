
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;
using Azure.Messaging.EventHubs;
using Azure.Messaging.EventHubs.Producer;
using Newtonsoft.Json.Linq;

// .Net Core Client program to send EventHub messages.
// Chris Joakim, 2020/07/02
//
// Use:
// $ dotnet run <sendMessagesBoolean> <messageCount>
// $ dotnet run false 1
// $ dotnet run true 10
//
// NuGet packages:
// dotnet add package Azure.Messaging.EventHubs --version 5.1.0
// dotnet add package Newtonsoft.Json
//
// See:
// https://github.com/Azure/azure-sdk-for-net
// https://docs.microsoft.com/en-us/dotnet/api/azure.messaging.eventhubs.producer.eventhubproducerclient?view=azure-dotnet
// https://docs.microsoft.com/en-us/azure/event-hubs/get-started-dotnet-standard-send-v2

namespace EventHubConsoleApp
{
    class Program
    {
        private static int epoch = 0;

        public static async Task Main(string[] args)
        {
            bool sendMessages = args[0].ToLower() == "true";
            int  messageCount = Int32.Parse(args[1]);
            Console.WriteLine("CLI Arg - sendMessages: " + sendMessages);
            Console.WriteLine("CLI Arg - messageCount: " + messageCount);

            List<JObject> allZipcodes = readZipcodesFile();
            List<string> randomZipcodes = selectRandomZipcodes(messageCount, allZipcodes);

            if (sendMessages) {
                await sendMessageBatch(randomZipcodes);
            }
        }

        private static List<JObject> readZipcodesFile() 
        {
            string filePath = "data/nc_zipcodes.json";
            List<JObject> zipCodeList = new List<JObject>();

            try  
            {  
                string text = System.IO.File.ReadAllText(filePath); 
                Console.WriteLine("read file: " + filePath);
                JArray array = JArray.Parse(text.Trim()); 
                foreach (JObject zipcode in array) {
                    zipCodeList.Add(zipcode);
                }
            }  
            catch (Exception ex)  
            {  
                Console.WriteLine(ex.Message);  
            }
            return zipCodeList; 
        }

        private static List<string> selectRandomZipcodes(int messageCount, List<JObject> allZipcodes)
        {
            List<string> randomList = new List<string>();
            int maxIndex = allZipcodes.Count - 1;
            Console.WriteLine("selectRandomZipcodes, maxIndex: " + maxIndex);
            Random random = new Random();
            TimeSpan ts = DateTime.UtcNow - new DateTime(1970, 1, 1);
            epoch = (int) ts.TotalSeconds;
            string timestamp = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ss.fffffffZ");

            while (randomList.Count < messageCount) {
                int randomIndex = random.Next(0, maxIndex);
                JObject zipcode = allZipcodes[randomIndex];

                // Remove these attributes so that the Adds don't faile
                zipcode.Remove("pk");
                zipcode.Remove("seq");
                zipcode.Remove("index");
                zipcode.Remove("timestamp");
                zipcode.Remove("epoch");
                zipcode.Remove("sender");

                zipcode.Add("pk", zipcode.Property("postal_cd").Value);
                zipcode.Add("seq", randomList.Count + 1);
                zipcode.Add("index", randomIndex);
                zipcode.Add("timestamp", timestamp);
                zipcode.Add("epoch", epoch);
                zipcode.Add("sender", "dotnet_core_sdk");
                string jsonStr = zipcode.ToString();
                Console.WriteLine(jsonStr);
                randomList.Add(jsonStr);
            }
            Console.WriteLine("selectRandomZipcodes contains " + randomList.Count);
            return randomList;
        }

        private static async Task sendMessageBatch(List<string> messages) {

            string connString   = Environment.GetEnvironmentVariable("AZURE_STREAMPOC_EVENTHUB_CONN_STRING");
            string eventHubName = Environment.GetEnvironmentVariable("AZURE_STREAMPOC_EVENTHUB_HUBNAME");
            Console.WriteLine("sendMessageBatch, connString:   " + connString);
            Console.WriteLine("sendMessageBatch, eventHubName: " + eventHubName);

            await using (var producerClient = new EventHubProducerClient(connString, eventHubName))
            {
                using EventDataBatch eventBatch = await producerClient.CreateBatchAsync();
                foreach (string message in messages) {
                    eventBatch.TryAdd(new EventData(Encoding.UTF8.GetBytes(message)));
                }
                Console.WriteLine("Sending message batch of " + messages.Count);
                await producerClient.SendAsync(eventBatch);
                Console.WriteLine("The batch of messages has been sent");
                Console.WriteLine("Query CosmosDB with: SELECT * FROM c where c.sender = 'dotnet_core_sdk' and c.epoch >= " + epoch);
//print("query cosmosdb with: SELECT * FROM c where c.sender = '{}' and c.epoch >= {}".format('python_kafka_sdk', start_epoch))
            }
        }
    }
}
