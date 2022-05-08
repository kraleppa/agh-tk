defmodule Scraper.Sender do
  use GenServer
  use AMQP
  require Logger

  @channel_name :sender
  @exchange_name Application.get_env(:scraper, :exchange_name)
  @info_exchange Application.get_env(:scraper, :info_exchange)

  def start_link(_args \\ %{}) do
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
    Map.put(json, "fileState", %{"fileFound" => true})
      |> Poison.encode()
      |> case do
        {:ok, string_json} ->
          Basic.publish(channel, @exchange_name, key, string_json)
          Logger.info("File sent to the extractor")

          Basic.publish(channel, @info_exchange, "result", string_json)
          Logger.info("Info sent to result exchange")

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
