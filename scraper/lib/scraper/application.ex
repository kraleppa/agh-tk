defmodule Scraper.Application do
  use Application

  require Logger

  def start(_type, _args) do
    Logger.info("Hello from scraper")
    opts = [strategy: :one_for_one, name: Scraper.Supervisor]
    Supervisor.start_link([], opts)
  end
end
