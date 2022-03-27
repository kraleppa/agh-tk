defmodule Scraper.Application do
  use Application
  require Logger

  alias Scraper.Receiver
  alias Scraper.Sender

  def start(_type, _args) do
    opts = [strategy: :one_for_one, name: Scraper.Supervisor]

    children = [
      Receiver,
      Sender,
      {Task.Supervisor, name: Scraper.WorkerSupervisor}
    ]

    Supervisor.start_link(children, opts)
  end
end
