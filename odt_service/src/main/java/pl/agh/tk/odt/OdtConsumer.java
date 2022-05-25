package pl.agh.tk.odt;

import com.rabbitmq.client.AMQP;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.DefaultConsumer;
import com.rabbitmq.client.Envelope;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.nio.charset.StandardCharsets;

public class OdtConsumer extends DefaultConsumer {

    private static final Logger logger = LoggerFactory.getLogger(OdtConsumer.class);

    private final Channel channelOut;
    public OdtConsumer(Channel channelIn, Channel channelOut) {
        super(channelIn);
        this.channelOut = channelOut;
    }

    @Override
    public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) throws IOException {
        if(body != null){
            JSONObject json = new JSONObject(new String(body,  StandardCharsets.UTF_8));
            String extractedText = OdtSearcher.getText(json.getString("file"));
            setState(json, extractedText);

            channelOut.basicPublish(
                    "text",
                    "text",
                    new AMQP.BasicProperties(),
                    json.toString().getBytes(StandardCharsets.UTF_8)
            );

            logger.info("sent response with {}", json);

        }
    }

    private void setState(JSONObject json, String extractedText) {
        JSONObject fileState = getJsonObject(json);
        if (extractedText != null) {
            json.put("text", extractedText);
            fileState.put("fileProcessed", true);
        } else {
            json.put("text", "");
            fileState.put("fileProcessingError", true);
        }
        json.put("fileState", fileState);
    }

    private JSONObject getJsonObject(JSONObject json) {
        return json.has("fileState") ?
                (JSONObject) json.get("fileState") : new JSONObject();

    }
}
