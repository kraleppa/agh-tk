import React from "react";
import { Box, Badge, Flex, Heading, Grid, GridItem } from "@chakra-ui/react";
import { fileTypes } from "../../utils/file-types";
import Highlighter from "react-highlight-words";

const Result = ({ filePath, fileFormat, text, words }) => {
  const badgeBackgroundColor = fileTypes[fileFormat]?.color;

  const chunkPadding = 100;
  const chunks = [];

  const allOccurrences = words
    .reduce((occurrences, word) => {
      const wordOccurrences = [...text.matchAll(new RegExp(word, "gi"))].map(
        (match) => match.index
      );

      return [...occurrences, ...wordOccurrences];
    }, [])
    .sort((a, b) => a - b);

  let startChunkIndex = 0;
  let endChunkIndex = 0;
  for (let i = 0; i < allOccurrences.length; i++) {
    if (allOccurrences[i + 1] - allOccurrences[i] <= chunkPadding) {
      endChunkIndex = i;
    } else {
      chunks.push(
        text.slice(
          Math.max(allOccurrences[startChunkIndex] - chunkPadding, 0),
          allOccurrences[endChunkIndex] + chunkPadding
        )
      );
      startChunkIndex = i + 1;
      endChunkIndex = i + 1;
    }
  }

  return (
    <Grid templateColumns="repeat(12, 1fr)" gap={4}>
      <GridItem colSpan={5}>
        <Box py="4">
          <Heading size="sm">{filePath}</Heading>
        </Box>
      </GridItem>
      <GridItem colSpan={1}>
        <Box py="4">
          <Heading size="sm">{allOccurrences.length}</Heading>
        </Box>
      </GridItem>
      <GridItem colSpan={5}>
        <Box py="4">
          {chunks.map((chunk) => (
            <Box pb="2">
              <cite>
                ...
                <Highlighter
                  searchWords={words}
                  autoEscape
                  textToHighlight={chunk}
                />
                ...
              </cite>
            </Box>
          ))}
        </Box>
      </GridItem>
      <GridItem colSpan={1}>
        <Flex height="100%" alignItems="center" justifyContent="flex-end">
          <Badge background={badgeBackgroundColor}>{fileFormat}</Badge>
        </Flex>
      </GridItem>
    </Grid>
  );
};

export default Result;
