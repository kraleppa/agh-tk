package pl.agh.tk.odt;

import org.apache.tika.exception.TikaException;
import org.apache.tika.metadata.Metadata;
import org.apache.tika.parser.ParseContext;
import org.apache.tika.parser.odf.OpenDocumentParser;
import org.apache.tika.sax.BodyContentHandler;
import org.xml.sax.SAXException;
import org.slf4j.Logger;

import org.slf4j.LoggerFactory;

import java.io.FileInputStream;
import java.io.IOException;


public class OdtSearcher {

    private static final Logger logger = LoggerFactory.getLogger(OdtSearcher.class);

    static String getText(String path) {
        BodyContentHandler handler = new BodyContentHandler();

        Metadata metadata = new Metadata();
        FileInputStream inputstream = null;
        try {
            inputstream = new FileInputStream(path);

            ParseContext pcontext = new ParseContext();

            //Open Document Parser
            OpenDocumentParser openofficeparser = new OpenDocumentParser();

            openofficeparser.parse(inputstream, handler, metadata, pcontext);
        } catch (IOException | SAXException | TikaException e) {
            throw new RuntimeException(e);
        }

        return handler.toString();
    }
}
