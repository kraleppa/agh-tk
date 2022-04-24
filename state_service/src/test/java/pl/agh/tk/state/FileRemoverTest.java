package pl.agh.tk.state;

import org.apache.commons.io.FileUtils;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.io.IOException;

import static org.junit.jupiter.api.Assertions.*;

class FileRemoverTest {

    private final static String DIR_PATH = "./testDir";

    private final static String TEST_DIR_PATH = DIR_PATH + "/dir1";

    private final static String FILE_1_PATH = TEST_DIR_PATH + "/file1.txt";

    private final static String FILE_2_PATH = TEST_DIR_PATH + "/file2.bmp";

    @BeforeEach
    public void setUp() throws IOException {
        File file1 = new File(FILE_1_PATH);
        File file2 = new File(FILE_2_PATH);
        FileUtils.createParentDirectories(file1);
        file1.createNewFile();
        FileUtils.createParentDirectories(file2);
        file2.createNewFile();
    }

    @Test
    public void shouldRemoveOnlyFile() throws IOException {
        // given
        FileRemover fileRemover = new FileRemover();
        File file = new File(FILE_1_PATH);

        // when
        assertTrue(file.exists());
        fileRemover.deleteFile(FILE_1_PATH);

        // then
        assertFalse(file.exists());
        File otherFile = new File(FILE_2_PATH);
        assertTrue(otherFile.exists());
    }

    @Test
    public void shouldRemoveFilesAndParentDirectory() throws IOException {
        // given
        FileRemover fileRemover = new FileRemover();
        File file1 = new File(FILE_1_PATH);
        File file2 = new File(FILE_2_PATH);

        // when
        assertTrue(file1.exists());
        assertTrue(file2.exists());
        fileRemover.deleteFile(FILE_1_PATH);
        fileRemover.deleteFile(FILE_2_PATH);

        // then
        assertFalse(file1.exists());
        assertFalse(file2.exists());
        File directory = new File(TEST_DIR_PATH);
        assertFalse(directory.exists());
        File mainDirectory = new File(DIR_PATH);
        assertTrue(mainDirectory.exists());
    }

    @AfterEach
    public void cleanUp() throws IOException {
        File directory = new File("./testDir");
        if (directory.exists()) {
            FileUtils.deleteDirectory(directory);
        }
    }
}