import { Box, Container, Heading, SimpleGrid } from "@chakra-ui/react";
import { RabbitMQConnection } from "./webSockets/RabbitMQConnection";
import { useEffect, useState } from "react";
import Results from "./Components/results/results";
import Form from "./Components/form/form";
import { isArchivePath } from "./utils";

function App() {
  const [results, setResults] = useState([]);

  const addResult = (newResult) => {
    console.log("NEW RESULT: ", newResult);

    const resultParsed = {
      originalFile: "",
      fileState: {
        textFound: newResult.found,
        fileFound: newResult.fileState?.fileFound,
      },
    };
    if (!!newResult.video) {
      resultParsed.originalFile = newResult.originalFile;
    } else if (!!newResult.archive) {
      resultParsed.originalFile = newResult.archive.filePathInArchive;
    } else {
      resultParsed.originalFile = newResult.file;
    }

    if (!isArchivePath(resultParsed.originalFile)) {
      setResults((oldResults) => [
        ...oldResults.filter(
          (x) => x.originalFile !== resultParsed.originalFile
        ),
        resultParsed,
      ]);
    }
  };

  const connection = new RabbitMQConnection(addResult);

  const onSubmit = ({ phrase, path }, fileFormats, searchModes) => {
    setResults([]);
    connection.sendRequest(
      phrase,
      path.replace(/\\/g, "/"),
      [...fileFormats],
      [...searchModes]
    );
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
          <Results results={results} />
        </SimpleGrid>
      </Container>
    </Box>
  );
}

export default App;
