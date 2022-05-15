import {
  Box,
  Checkbox,
  Divider,
  Flex,
  Grid,
  GridItem,
  Heading,
} from "@chakra-ui/react";
import { useState } from "react";
import Result from "./result";

const Results = ({ results }) => {
  const [showOnlyPhraseFound, setShowOnlyPhraseFound] = useState(false);

  return (
    <Box mt={8} borderRadius="5px">
      <Heading size="lg" mb={6}>
        Results
      </Heading>

      <Checkbox
        onChange={(e) => setShowOnlyPhraseFound(e.target.checked)}
        mb={6}
        colorScheme="purple"
      >
        Show only results with phrase found
      </Checkbox>

      <Grid templateColumns="repeat(12, 1fr)" gap={4}>
        <GridItem colSpan={8}>
          <Box py="4">
            <Heading size="md">File path</Heading>
          </Box>
        </GridItem>
        <GridItem colSpan={3}>
          <Box py="4">
            <Heading size="md">Result</Heading>
          </Box>
        </GridItem>
        <GridItem colSpan={1}>
          <Flex height="100%" alignItems="center" justifyContent="flex-end">
            <Heading size="md">Format</Heading>
          </Flex>
        </GridItem>
      </Grid>

      <Divider borderColor="gray.300" />

      {!!results
        ? results
            .filter((res) =>
              showOnlyPhraseFound
                ? res.parsedFileState === "PHRASE_FOUND"
                : true
            )
            .map((result, i) => (
              <div key={`${result.originalFile}-${i}`}>
                <Result
                  filePath={result.originalFile}
                  fileFormat={result.originalFile.split(".").pop()}
                  parsedFileState={result.parsedFileState}
                ></Result>
                {i < results.length - 1 ? (
                  <Divider borderColor="gray.300" />
                ) : null}
              </div>
            ))
        : null}
    </Box>
  );
};

export default Results;
