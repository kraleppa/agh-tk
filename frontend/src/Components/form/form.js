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
import { fileTypes } from "../../utils/file-types";

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
      path: "",
    },
  });

  const possibleFileTypes = Object.keys(fileTypes).map((type) => `.${type}`);

  const searchModes = ["synonyms", "typos", "forms", "translations"];
  const languages = ["English", "German"];

  const [selectedFileTypes, setSelectedFileTypes] = useState([]);
  const [selectedSearchModes, setSelectedSearchModes] = useState([]);
  const [selectedLanguages, setSelectedLanguages] = useState([]);

  const resetForm = () => {
    reset();
    setSelectedFileTypes([]);
    setSelectedSearchModes([]);
  };

  const handlePathSelect = () => {
    window.api.selectFolder().then((result) => {
      if (!!result) {
        resetField("path");
        setValue("path", result);
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
        onSubmit(data.phrase, data.path, selectedFileTypes, selectedSearchModes, selectedLanguages)
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

        <FormControl isInvalid={errors.path}>
          <FormLabel htmlFor="path">Directory path</FormLabel>
          <InputGroup flex flexDirection="column">
            <Input
              id="path"
              placeholder="Enter directory path"
              {...register("path", {
                required: "Directory path is required",
              })}
              type="text"
              pr="4.5rem"
              {...inputStyles}
            />
            <FormErrorMessage>
              {errors.path && errors.path.message}
            </FormErrorMessage>
            <InputRightElement width="4.5rem">
              <Button size="sm" onClick={handlePathSelect}>
                Select
              </Button>
            </InputRightElement>
          </InputGroup>
        </FormControl>

        <FormControl py={0}>
          <FormLabel>File types</FormLabel>
          <MultiSelectMenu
            selectedOptions={selectedFileTypes}
            setSelectedOptions={setSelectedFileTypes}
            label="File types"
            options={[...possibleFileTypes]}
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

        <FormControl py={0}>
          <FormLabel>Languages</FormLabel>
          <MultiSelectMenu
            selectedOptions={selectedLanguages}
            setSelectedOptions={setSelectedLanguages}
            label="Languages"
            options={[...languages]}
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
              Clear fields
            </Button>
          </Stack>
        </ButtonGroup>
      </Stack>
    </form>
  );
};

export default Form;
