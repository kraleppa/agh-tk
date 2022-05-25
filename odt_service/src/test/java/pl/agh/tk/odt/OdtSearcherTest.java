package pl.agh.tk.odt;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import org.junit.jupiter.api.Test;

import java.nio.file.Paths;

public class OdtSearcherTest {

    @Test
    void testSearching(){
        String text = OdtSearcher.getText(Paths.get("src", "test", "resources", "bells.odt").toString());
        assertThat(text).contains("Lonely path across the marshland");
        assertThat(text).contains("In bleak morning light");
    }
}
