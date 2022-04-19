package pl.agh.tk.state;

import org.apache.commons.io.FileUtils;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public final class Utils {

    public static final String HOST = "rabbitmq";
//    public static final String HOST = "localhost";

    public static final String QUEUE_NAME = "state";

    public static final String VIDEO_KEY = "video";

    public static final String FRAME_PATH_KEY = "framePath";

    public static final String ARCHIVE_KEY = "archive";

    public static final String PATH_IN_VOLUME_KEY = "filePathInVolume";

    public static final String PATH_KEY = "path";

    public static String getParentDirectory(String path) {
        // ex: path = "~/extracted/dir1/file1.txt"
        List<String> parts = Arrays.stream(path.split("/")).collect(Collectors.toList());
        if (parts.size() < 4) {
            // no directories to be removed
            return null;
        }
        parts.remove(parts.size() - 1);
        return String.join("/", parts);
    }

    public static String getValidPath(String path) {
        String userDirectoryPath = FileUtils.getUserDirectoryPath().replace("\\", "/");
        return path.replaceFirst("/host", userDirectoryPath);
    }
}