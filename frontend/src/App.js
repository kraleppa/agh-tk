import {
  Box,
  Button,
  Center,
  Container,
  Heading,
  SimpleGrid,
} from "@chakra-ui/react";
import SearchBar from "./Components/SearchBar";
import data from "./data.json";
import { RabbitMQConnection } from "./webSockets/RabbitMQConnection";
import { useEffect, useState } from "react";
import ShowResults from "./Components/ShowResults";
import DirectoryPicker from "./Components/directory-picker/directory-picker";

function App() {
  const [results, setResults] = useState(data);
  const clearResults = () => setResults([]);
  const addResult = (newResult) => {
    console.log("adding result: " + JSON.stringify(newResult));
    setResults((oldResults) => [...oldResults, newResult]);
  };

  const connection = new RabbitMQConnection(addResult);

  const onClick = () => {
    clearResults();
    // todo replace hardcoded request
    connection.sendRequest("dog", ["docx"], ["forms"]);
  };

  useEffect(() => {
    console.dir(results);
  }, [results]);

  return (
    <Box bg="gray.600" h="100vh">
      <Container maxW="container.xl">
        <SimpleGrid columns={1} spacing={5}>
          <Center bg="purple.500" h="100px" color="white">
            <Heading>FileFinder</Heading>
          </Center>
          <SearchBar connection={connection} clearResults={clearResults} />
          <DirectoryPicker />
          <Center>
            <Button colorScheme="purple" variant="solid" onClick={onClick}>
              Search
            </Button>
          </Center>
          <Center>
            <ShowResults results={results} />
          </Center>
        </SimpleGrid>
      </Container>
    </Box>
  );
}

export default App;
