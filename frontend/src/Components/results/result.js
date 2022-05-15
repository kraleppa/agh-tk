import { Box, Badge, Flex, Heading, Grid, GridItem } from "@chakra-ui/react";
import { fileFormats } from "./file-formats";

const Result = ({ path, fileFormat, parsedFileState }) => {
  const badgeBackgroundColor = fileFormats.find(
    (format) => format.value === fileFormat
  )?.color;

  const fileStateMap = {
    PHRASE_FOUND: "Phrase found",
    PHRASE_NOT_FOUND: "Phrase not found",
    FILE_PROCESSED: "File processed",
    FILE_ERROR: "Error",
    FILE_PROCESSING: "Processing...",
  };

  return (
    <Grid templateColumns="repeat(12, 1fr)" gap={4}>
      <GridItem colSpan={8}>
        <Box py="4">
          <Heading size="sm">{path}</Heading>
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
