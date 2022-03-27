defmodule Scraper.Application do
  use Application
  require Logger

  alias Scraper.Receiver

  def start(_type, _args) do
    opts = [strategy: :one_for_one, name: Scraper.Supervisor]

    children = [
      Receiver,
      {Task.Supervisor, name: Scraper.WorkerSupervisor}
    ]

    Supervisor.start_link(children, opts)
  end
end
