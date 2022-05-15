import { Box, Container, Heading, SimpleGrid } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import Results from "./Components/results/results";
import Form from "./Components/form/form";
import {
  isArchivePath,
  parseResult,
  resultShouldBeReplaced,
  sendRequest,
} from "./utils";
import { Client } from "@stomp/stompjs";

function App() {
  const [results, setResults] = useState([]);
  const [client, setClient] = useState();

  useEffect(() => {
    const client = new Client({
      brokerURL: "ws://localhost:15674/ws",
      reconnectDelay: 5000,
      heartbeatIncoming: 10000,
      heartbeatOutgoing: 10000,
    });
    client.onConnect = (frame) => {
      client.subscribe("/queue/result", onMessage);
      console.info("Connected successfully");
    };
    client.onWebSocketError = () => {
      console.error("Web Socket error");
    };
    client.onStompError = () => {
      console.error("Stomp error");
    };
    const onMessage = (message) => {
      if (message.body) {
        console.info("Received message: " + message.body);
        addResult(JSON.parse(message.body));
      } else {
        console.info("Received empty message");
      }
    };
    setClient(client);
    client.activate();
    return () => client.deactivate();
  }, []);

  const addResult = (result) => {
    const newResult = parseResult(result);

    const currentResult = results.find(
      (res) => res.originalFile === newResult.originalFile
    );

    if (
      !currentResult ||
      (!!currentResult && resultShouldBeReplaced(currentResult, newResult))
    ) {
      if (!isArchivePath(newResult.originalFile)) {
        setResults((oldResults) => [
          ...oldResults.filter(
            (x) => x.originalFile !== newResult.originalFile
          ),
          newResult,
        ]);
      }
    }
  };

  const onSubmit = (phrase, path, fileTypes, searchModes) => {
    setResults([]);
    sendRequest(client, phrase, path, fileTypes, searchModes);
  };

  return (
    <Box minHeight={"100vh"} bg="gray.50">
      <Container
        bg="gray.50"
        minHeight={"100vh"}
        py={6}
        px={6}
        maxW="container.lg"
      >
        <SimpleGrid columns={1} spacing={5}>
          <Box py={4} h="80px" color="purple.500">
            <Heading>FileFinder</Heading>
          </Box>
          <Form onSubmit={onSubmit} />
          <Results results={results} />
        </SimpleGrid>
      </Container>
    </Box>
  );
}

export default App;
