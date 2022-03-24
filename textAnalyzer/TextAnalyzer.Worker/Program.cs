using TextAnalyzer.Worker;

const string WorkerOptionsSectionName = "WorkerSettings";

var host = Host.CreateDefaultBuilder(args)
    .ConfigureServices((ctx, services) =>
    {
        services.Configure<WorkerOptions>(ctx.Configuration.GetSection(WorkerOptionsSectionName));
        services.AddHostedService<Worker>();
    })
    .Build();

await host.RunAsync();
