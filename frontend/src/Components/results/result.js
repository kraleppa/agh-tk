import { Box, Badge, Flex, Heading, Grid, GridItem } from "@chakra-ui/react";
import { fileTypes } from "../../utils/file-types";
import Highlighter from "react-highlight-words";

const Result = ({ filePath, fileFormat, text, words, routingKey }) => {
  const badgeBackgroundColor = fileTypes[fileFormat]?.color;
  const filePathHeading =
    fileFormat === "mp4"
      ? `${filePath} (${
          routingKey.includes("unconverted") ? "audio" : "video"
        })`
      : filePath;

  return (
    <Grid templateColumns="repeat(12, 1fr)" gap={4}>
      <GridItem colSpan={6}>
        <Box py="4">
          <Heading size="sm">{filePathHeading}</Heading>
        </Box>
      </GridItem>
      <GridItem colSpan={5}>
        <Box py="4">
          <Highlighter searchWords={words} autoEscape textToHighlight={text} />
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
