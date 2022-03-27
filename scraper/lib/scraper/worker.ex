defmodule Scraper.Worker do
  require Logger

  def run(%{path: path, file_types: file_types} = args) do
    Logger.info("Traversing started for #{path}")

    Path.wildcard(path)
    |> Enum.filter(&filter(&1, file_types))
    |> IO.inspect()
  end

  defp filter(path, []), do: true

  defp filter(path, list) do
    format = Path.extname(path)
    Enum.member?(list, format)
  end
end
