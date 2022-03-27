defmodule Scraper.Sender do
  use GenServer
  use AMQP
  require Logger

  @channel_name :sender
  @exchange_name Application.get_env(:scraper, :exchange_name)

  def start_link(args \\ %{}) do
    GenServer.start(__MODULE__, %{}, name: __MODULE__)
  end

  @impl true
  def init(args) do
    channel = get_channel()
    {:ok, Map.put(args, :channel, channel)}
  end

  def send(json, key) do
    GenServer.cast(__MODULE__, {:send, json, key})
  end

  @impl true
  def handle_cast({:send, json, key}, %{channel: channel} = state) do
    case Poison.encode(json) do
      {:ok, string_json} ->
        Basic.publish(channel, @exchange_name, key, string_json)
        Logger.info("File sent to the extractor")

      _ ->
        Logger.error("Could not parse result json")
    end

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
end
