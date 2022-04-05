import React, { useState } from "react";
import {
  Button,
  ButtonGroup,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Input,
  InputGroup,
  InputRightElement,
  Stack,
  Textarea,
} from "@chakra-ui/react";
import MultiSelectMenu from "./multi-select-menu";
import { useForm } from "react-hook-form";

const Form = ({ onSubmit }) => {
  const {
    register,
    reset,
    setValue,
    handleSubmit,
    resetField,
    formState: { errors, isSubmitting },
  } = useForm({
    defaultValues: {
      phrase: "",
      directory: "",
    },
  });

  const fileFormats = [
    "pptx",
    "docx",
    "txt",
    "jpeg",
    "jpg",
    "png",
    "mp4",
    "zip",
  ];
  const searchModes = ["synonyms", "typos", "forms"];

  const [selectedFileFormats, setSelectedFileFormats] = useState([]);
  const [selectedSearchModes, setSelectedSearchModes] = useState([]);

  const resetForm = () => {
    reset();
    setSelectedFileFormats([]);
    setSelectedSearchModes([]);
  };

  const handleDirectorySelect = () => {
    window.api.selectFolder().then((result) => {
      if (!!result) {
        resetField("directory");
        setValue("directory", result);
      }
    });
  };

  const inputStyles = {
    borderColor: "purple.300",
    focusBorderColor: "purple.400",
    bg: "white",
  };

  return (
    <form
      onSubmit={handleSubmit((data) =>
        onSubmit(data, selectedFileFormats, selectedSearchModes)
      )}
    >
      <Stack spacing={3}>
        <FormControl isInvalid={errors.phrase}>
          <FormLabel htmlFor="phrase">Phrase</FormLabel>
          <Textarea
            id="phrase"
            placeholder="Enter phrase"
            {...register("phrase", {
              required: "Phrase is required",
            })}
            type="text"
            {...inputStyles}
          />
          <FormErrorMessage>
            {errors.phrase && errors.phrase.message}
          </FormErrorMessage>
        </FormControl>

        <FormControl isInvalid={errors.directory}>
          <FormLabel htmlFor="directory">Directory</FormLabel>
          <InputGroup flex flexDirection="column">
            <Input
              id="directory"
              placeholder="Enter directory path"
              {...register("directory", {
                required: "Directory path is required",
              })}
              type="text"
              pr="4.5rem"
              {...inputStyles}
            />
            <FormErrorMessage>
              {errors.directory && errors.directory.message}
            </FormErrorMessage>
            <InputRightElement width="4.5rem">
              <Button size="sm" onClick={handleDirectorySelect}>
                Select
              </Button>
            </InputRightElement>
          </InputGroup>
        </FormControl>

        <FormControl py={0}>
          <FormLabel>File formats</FormLabel>
          <MultiSelectMenu
            selectedOptions={selectedFileFormats}
            setSelectedOptions={setSelectedFileFormats}
            label="File formats"
            options={[...fileFormats]}
          />
        </FormControl>

        <FormControl py={0}>
          <FormLabel>Phrase search modes</FormLabel>
          <MultiSelectMenu
            selectedOptions={selectedSearchModes}
            setSelectedOptions={setSelectedSearchModes}
            label="Phrase search modes"
            options={[...searchModes]}
          />
        </FormControl>

        <ButtonGroup>
          <Stack spacing={[2, 4]} mt={4} direction={["column", "row"]}>
            <Button colorScheme="purple" isLoading={isSubmitting} type="submit">
              Submit
            </Button>
            <Button
              colorScheme="purple"
              variant="outline"
              onClick={() => resetForm()}
            >
              Reset form
            </Button>
          </Stack>
        </ButtonGroup>
      </Stack>
    </form>
  );
};

export default Form;
