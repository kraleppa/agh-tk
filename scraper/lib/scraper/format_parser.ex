defmodule Scraper.FormatParser do
  @keys %{
    ".pptx" => ["format.microsoft.pptx"],
    ".docx" => ["format.microsoft.docx"],
    ".txt" => ["format.txt"],
    ".jpeg" => ["format.image.jpeg"],
    ".jpg" => ["format.image.jpeg"],
    ".png" => ["format.image.png"],
    ".mp4" => ["format.movie.mp4", "format.unconverted.mp4"],
    ".zip" => ["format.archive.zip"],
    ".tar" => ["format.archive.tar"],
    ".gz" => ["format.archive.gz"],
    ".wav" => ["format.audio.wav"],
    ".mp3" => ["format.unconverted.mp3"],
    ".odf" => ["format.opendoc.odf"],
    ".odt" => ["format.opendoc.odt"],
    ".pdf" => ["format.pdf"]
  }

  def get_key(format), do: Map.get(@keys, format)
end
