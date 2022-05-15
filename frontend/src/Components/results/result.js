import { Box, Badge, Flex, Heading, Grid, GridItem } from "@chakra-ui/react";
import { fileTypes } from "../../utils/file-types";

const Result = ({ filePath, fileFormat, parsedFileState }) => {
  const badgeBackgroundColor = fileTypes[fileFormat]?.color;

  const fileStateMap = {
    PHRASE_FOUND: "Phrase found",
    PHRASE_NOT_FOUND: "Phrase not found",
    PROCESSED: "File processed",
    ERROR: "Error",
    PROCESSING: "Processing...",
  };

  return (
    <Grid templateColumns="repeat(12, 1fr)" gap={4}>
      <GridItem colSpan={8}>
        <Box py="4">
          <Heading size="sm">{filePath}</Heading>
        </Box>
      </GridItem>
      <GridItem colSpan={3}>
        <Box py="4">
          <Heading size="sm">{fileStateMap[parsedFileState] || ""}</Heading>
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
