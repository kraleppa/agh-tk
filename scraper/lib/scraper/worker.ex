defmodule Scraper.Worker do
  require Logger

  def run(%{path: path} = args) do
    Logger.info("Traversing started for #{path}")

    Path.wildcard(path)
    |> IO.inspect()
  end
end
