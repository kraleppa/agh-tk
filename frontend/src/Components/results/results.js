import {
  Box,
  Checkbox,
  Divider,
  Flex,
  Grid,
  GridItem,
  Heading,
  Progress,
  Text,
} from "@chakra-ui/react";
import React, { useState } from "react";
import Result from "./result";

const Results = ({ results = [] }) => {
  const resultsWithPhraseFound = results.filter(
    (result) => result.parsedFileState === "PHRASE_FOUND"
  );

  const counts = results.reduce(
    (acc, result) => {
      acc[result.parsedFileState]++;
      return acc;
    },
    {
      PROCESSING: 0,
      PROCESSED: 0,
      PHRASE_FOUND: 0,
      PHRASE_NOT_FOUND: 0,
      ERROR: 0,
    }
  );

  const completedCount =
    counts.ERROR + counts.PHRASE_NOT_FOUND + counts.PHRASE_FOUND;

  const isAllCompleted = completedCount === results.length;

  return (
    <Box mt={8} borderRadius="5px">
      <Heading size="lg" mb={6}>
        Results
      </Heading>

      {results.length > 0 && (
        <React.Fragment>
          <Progress
            hasStripe
            isAnimated={!isAllCompleted}
            min={0}
            max={results.length}
            value={completedCount}
            colorScheme={isAllCompleted ? "green" : "blue"}
          />
          <Text fontSize="xl" align="center" my={2}>
            {!isAllCompleted
              ? `Processed ${completedCount} of ${results.length} files`
              : "All files processed!"}
          </Text>
        </React.Fragment>
      )}

      <Grid templateColumns="repeat(12, 1fr)" gap={4}>
        <GridItem colSpan={5}>
          <Box py="4">
            <Heading size="md">File path</Heading>
          </Box>
        </GridItem>
        <GridItem colSpan={1}>
          <Box py="4">
            <Heading size="md">Matches</Heading>
          </Box>
        </GridItem>
        <GridItem colSpan={5}>
          <Box py="4">
            <Heading size="md">Fragments with found text</Heading>
          </Box>
        </GridItem>
        <GridItem colSpan={1}>
          <Flex height="100%" alignItems="center" justifyContent="flex-end">
            <Heading size="md">Format</Heading>
          </Flex>
        </GridItem>
      </Grid>

      <Divider borderColor="gray.300" />

      {resultsWithPhraseFound.map((result, i) => (
        <div key={`${result.originalFile}-${i}`}>
          <Result
            filePath={result.originalFile}
            fileFormat={result.originalFile.split(".").pop()}
            text={result.text}
            words={result.words}
          />
          {i < results.length - 1 ? <Divider borderColor="gray.300" /> : null}
        </div>
      ))}
    </Box>
  );
};

export default Results;
