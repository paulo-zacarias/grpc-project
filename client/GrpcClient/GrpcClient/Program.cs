using Grpc.Core;
using Grpc.Net.Client;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Hosting;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace GrpcClient
{
    class Program
    {
        static async Task Main(string[] args)
        {
            // The port number(5001) must match the port of the gRPC server.
            using var channel = GrpcChannel.ForAddress("http://localhost:50051");
            var client = new ChatApp.ChatAppClient(channel);

            using (var call = client.receiveMessages(new StartRequest { Name = "fooBar" }))
            {
                string messages = "";
                // If the server disconnects before closing the stream, client will throw exception
                try
                {
                    while (await call.ResponseStream.MoveNext())
                    {
                        var message = call.ResponseStream.Current;
                        messages += message.Msg;

                        //Console.WriteLine($"{message.Msg}");
                        Console.Clear();
                        Console.WriteLine(messages);
                    }
                }
                catch (RpcException)
                {
                    Console.WriteLine("Server disconnected");
                    return;
                }
                catch (Exception)
                {
                    Console.WriteLine("Something bad happend :(");
                    return;
                }
            }
            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();
        }
    }
}
