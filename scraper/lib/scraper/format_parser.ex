defmodule Scraper.FormatParser do
  @keys %{
    ".pptx" => "format.microsoft.pptx",
    ".docx" => "format.microsoft.docx",
    ".txt" => "format.txt",
    ".jpeg" => "format.image.jpeg",
    ".jpg" => "format.image.jpeg",
    ".png" => "format.image.png",
    ".mp4" => "format.movie.mp4",
    ".zip" => "format.movie.mov"
  }

  def get_key(format), do: Map.get(@keys, format)
end
