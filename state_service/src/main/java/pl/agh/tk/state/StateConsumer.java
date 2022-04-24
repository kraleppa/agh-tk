package pl.agh.tk.state;

import com.rabbitmq.client.AMQP;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.DefaultConsumer;
import com.rabbitmq.client.Envelope;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;

import static pl.agh.tk.state.Utils.ARCHIVE_KEY;
import static pl.agh.tk.state.Utils.FRAME_PATH_KEY;
import static pl.agh.tk.state.Utils.PATH_IN_VOLUME_KEY;
import static pl.agh.tk.state.Utils.VIDEO_KEY;
import static pl.agh.tk.state.Utils.getValidPath;

public class StateConsumer extends DefaultConsumer {

    private final Logger logger = LoggerFactory.getLogger(this.getClass());

    private final FileRemover fileRemover;

    public StateConsumer(Channel channel) {
        super(channel);
        this.fileRemover = new FileRemover();
    }

    @Override
    public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties,
                               byte[] body) throws IOException {
        if (body != null) {
            JSONObject msg = new JSONObject(new String(body));
            extractPathAndDeleteIfPossible(msg, VIDEO_KEY, FRAME_PATH_KEY);
            extractPathAndDeleteIfPossible(msg, ARCHIVE_KEY, PATH_IN_VOLUME_KEY);
        }
    }

    private void extractPathAndDeleteIfPossible(JSONObject json, String propKey, String valueKey) throws IOException {
        if (json.has(propKey)) {
            JSONObject prop = (JSONObject) json.get(propKey);
            String path = prop.getString(valueKey);
            logger.info("Trying to delete file '{}'", path);
            fileRemover.deleteFile(getValidPath(path));
        }
    }
}
