defmodule Scraper.Application do
  use Application
  require Logger

  alias Scraper.Receiver
  alias Scraper.Sender

  @env Application.get_env(:scraper, :env)

  def start(_type, _args) do
    opts = [strategy: :one_for_one, name: Scraper.Supervisor]

    # todo this has to be changed
    children = if @env == :test do
      []
    else
      [Receiver, Sender, {Task.Supervisor, name: Scraper.WorkerSupervisor}]
    end



    Supervisor.start_link(children, opts)
  end
end
