import { Table, Thead, Tr, Th, Td, Tbody } from "@chakra-ui/react";

export default function ShowResults({ results }) {
  const rows = results.map((result, key) => {
    return (
      <Tr key={key + "_" + result.path} textColor={() => key % 2 === 0 ? colors.black : colors.white}>
        <Td textAlign="center">{result.path}</Td>
        <Td textAlign="center">{result.found}</Td>
      </Tr>
    )
  })
  return (
    <Table variant="striped" colorScheme='purple' width="75%">
      <Thead>
        <Tr>
          <Th fontSize="large" textColor={colors.white} textAlign="center">FILE PATH</Th>
          <Th fontSize="large" textColor={colors.white} textAlign="center">WORD FOUND</Th>
        </Tr>
      </Thead>
      <Tbody>
        {rows}
      </Tbody>
    </Table>
  )
}

const colors = {
  black: "#000000",
  white: "#FFFFFF"
}
