defmodule Scraper.Receiver do
  use GenServer
  use AMQP
  require Logger

  @queue_name Application.get_env(:scraper, :queue_name)

  def start_link(args \\ %{}) do
    GenServer.start(__MODULE__, %{})
  end

  @impl true
  def init(args) do
    {:ok, channel} = AMQP.Application.get_channel(:mychan)
    {:ok, _consumer_tag} = Basic.consume(channel, @queue_name)


    {:ok, Map.put(args, :channel, channel)}
  end

  # This is a handler of messages form queue
  @impl true
  def handle_info({:basic_deliver, payload, %{delivery_tag: tag}}, %{channel: channel} = state) do
    Logger.info("Scraper received a new message #{payload}")

    # add logic here

    :ok = Basic.ack(channel, tag)
    {:noreply, state}
  end

  # Confirmation sent by the broker after registering this process as a consumer
  @impl true
  def handle_info({:basic_consume_ok, %{consumer_tag: consumer_tag}}, state) do
    {:noreply, state}
  end

  # Sent by the broker when the consumer is unexpectedly cancelled (such as after a queue deletion)
  @impl true
  def handle_info({:basic_cancel, %{consumer_tag: consumer_tag}}, state) do
    Logger.error("Connection lost (I guess)")
    {:stop, :normal, state}
  end

  # Confirmation sent by the broker to the consumer process after a Basic.cancel
  @impl true
  def handle_info({:basic_cancel_ok, %{consumer_tag: consumer_tag}}, state) do
    {:noreply, state}
  end
end
