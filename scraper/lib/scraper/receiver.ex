defmodule Scraper.Receiver do
  use GenServer
  use AMQP
  require Logger

  @queue_name Application.get_env(:scraper, :queue_name)
  @env Application.get_env(:scraper, :env)
  @channel_name :receiver

  def start_link(args \\ %{}) do
    GenServer.start(__MODULE__, %{})
  end

  @impl true
  def init(args) do
    channel = get_channel()
    {:ok, _consumer_tag} = Basic.consume(channel, @queue_name)

    {:ok, Map.put(args, :channel, channel)}
  end

  # This is a handler of messages form queue
  @impl true
  def handle_info({:basic_deliver, payload, %{delivery_tag: tag}}, %{channel: channel} = state) do
    Logger.info("Scraper received a new message #{payload}")

    with(
      {:ok, json} <- Poison.decode(payload),
      path when not is_nil(path) <- Map.get(json, "path"),
      file_types when not is_nil(file_types) <- get_in(json, ["filters", "fileTypes"]),
      parsed_path <- parse_path(path)
    ) do

      Task.Supervisor.start_child(
        Scraper.WorkerSupervisor,
        Scraper.Worker,
        :run,
        [%{path: parsed_path, file_types: file_types, json: json}]
      )
    else
      _ -> Logger.warn("Message ignored - wrong message format")
    end

    :ok = Basic.ack(channel, tag)
    {:noreply, state}
  end

  # Confirmation sent by the broker after registering this process as a consumer
  @impl true
  def handle_info({:basic_consume_ok, %{consumer_tag: _consumer_tag}}, state) do
    Logger.info("Scraper registered properly - waiting for messages...")
    {:noreply, state}
  end

  defp get_channel() do
    case AMQP.Application.get_channel(@channel_name) do
      {:ok, channel} ->
        channel

      {:error, _} ->
        Logger.error("Cannot connect to channel - retrying in 5 seconds...")
        :timer.sleep(5000)
        get_channel()
    end
  end

  defp parse_path(path) do
    case @env do
      :dev ->
        Path.expand(path) <> "/**"

      :prod ->
        res =
          Path.split(path)
          |> Enum.reject(&(&1 == "~"))
          |> Path.join()

        Application.get_env(:scraper, :root_directory) <> res <> "/**"
    end
  end
end
