package pl.agh.tk.state;

import org.apache.commons.io.FileUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.IOException;

public class FileRemover {

    private final Logger logger = LoggerFactory.getLogger(this.getClass());

    public void deleteFile(String path) throws IOException {
        File file = new File(path);
        if (file.exists()) {
            FileUtils.delete(file);
            logger.info("File '{}' has been removed", path);
            deleteDirectoryIfPossible(path);
        } else {
            logger.error("File '{}' doesn't exist - can't remove", path);
        }
    }

    private void deleteDirectoryIfPossible(String path) throws IOException {
        String parentDir = Utils.getParentDirectory(path);
        if (parentDir != null) {
            File directory = new File(parentDir);
            if (FileUtils.isEmptyDirectory(directory)) {
                boolean delete = directory.delete();
                if (delete) {
                    logger.info("Directory '{}' deleted - trying to delete parent directory", parentDir);
                    deleteDirectoryIfPossible(parentDir);
                } else {
                    logger.error("Could not delete directory '{}'", parentDir);
                }
            } else {
                logger.info("Parent directory of file '{}' is not empty", path);
            }
        }
    }
}
