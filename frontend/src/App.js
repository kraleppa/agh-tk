import { Box, Container, Heading, SimpleGrid } from "@chakra-ui/react";
import data from "./data.json";
import { RabbitMQConnection } from "./webSockets/RabbitMQConnection";
import { useEffect, useState } from "react";
import ShowResults from "./Components/ShowResults";
import Form from "./Components/form/Form";

function App() {
  const [results, setResults] = useState(data);
  const clearResults = () => setResults([]);
  const addResult = (newResult) => {
    console.log("adding result: " + JSON.stringify(newResult));
    setResults((oldResults) => [...oldResults, newResult]);
  };

  const connection = new RabbitMQConnection(addResult);

  const onSubmit = (data) => {
    // todo replace hardcoded request
    clearResults();
    connection.sendRequest("dog", ["docx"], ["forms"]);
  };

  useEffect(() => {
    console.dir(results);
  }, [results]);

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
          <ShowResults results={results} />
        </SimpleGrid>
      </Container>
    </Box>
  );
}

export default App;
