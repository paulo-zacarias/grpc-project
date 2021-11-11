using Grpc.Core;
using Grpc.Net.Client;
using Grpc.Net.Client.Configuration;
using System;
using System.Threading.Tasks;

namespace GrpcClient
{
    class Program
    {
        static async Task Main(string[] args)
        {
            // gRPC retries if server is not available
            //https://docs.microsoft.com/en-us/aspnet/core/grpc/retries?view=aspnetcore-6.0

            var defaultMethodConfig = new MethodConfig
            {
                Names = { MethodName.Default },
                RetryPolicy = new RetryPolicy
                {
                    MaxAttempts = 5,
                    InitialBackoff = TimeSpan.FromSeconds(1),
                    MaxBackoff = TimeSpan.FromSeconds(5),
                    BackoffMultiplier = 1.5,
                    RetryableStatusCodes = { StatusCode.Unavailable }
                }
            };

            using var channel = GrpcChannel.ForAddress("http://app-server:50051", new GrpcChannelOptions
            {
                ServiceConfig = new ServiceConfig { MethodConfigs = { defaultMethodConfig } }
            });

            var client = new ChatApp.ChatAppClient(channel);

            using (var call = client.receiveMessages(new StartRequest { Name = "fooBar" }))
            {
                // If the server disconnects before closing the stream, client will throw exception
                try
                {
                    // Manually cancel the call from client side
                    Console.CancelKeyPress += delegate
                    {
                        Console.WriteLine("Cancelling the call...");
                        call.Dispose();
                        Environment.Exit(0);
                    };
                    while (await call.ResponseStream.MoveNext())
                    {
                        var received = call.ResponseStream.Current;
                        Console.Write(received.Msg);
                    }
                }
                catch (RpcException ex)
                {
                    if (ex.StatusCode == StatusCode.Cancelled)
                        Console.WriteLine("\n\nServer has terminated the stream.");
                    if (ex.StatusCode == StatusCode.Unavailable)
                    {
                        Console.WriteLine("Server is not available.");
                    } 
                    else
                    {
                        Console.WriteLine($"Call ended with Status Code {ex.StatusCode}");
                    }
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
