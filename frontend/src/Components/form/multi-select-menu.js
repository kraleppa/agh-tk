import React from "react";
import {
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuDivider,
  MenuGroup,
  MenuOptionGroup,
  MenuItemOption,
  Button,
} from "@chakra-ui/react";
import { ChevronDownIcon } from "@chakra-ui/icons";

const MultiSelectMenu = ({ selectedOptions, setSelectedOptions, ...props }) => {
  const { label, options, buttonProps } = props;

  return (
    <Menu closeOnSelect={false}>
      {({ onClose }) => (
        <>
          <MenuButton
            as={Button}
            rightIcon={<ChevronDownIcon />}
            type="button"
            backgroundColor={"white"}
            color={selectedOptions.length ? "purple.500" : "gray.600"}
            borderColor={"purple.300"}
            borderWidth={1}
            p={4}
            _focus={{
              outline: "none",
            }}
            {...buttonProps}
          >
            {`${label}${
              selectedOptions.length > 0 ? ` (${selectedOptions.length})` : ""
            }`}
          </MenuButton>
          <MenuList>
            <MenuGroup title={undefined}>
              <MenuItem
                onClick={() => {
                  setSelectedOptions([]);
                  onClose();
                }}
              >
                Clear all
              </MenuItem>
            </MenuGroup>
            <MenuDivider />
            <MenuOptionGroup
              mt={100}
              title={undefined}
              value={selectedOptions}
              type="checkbox"
              onChange={(values) => {
                setSelectedOptions(values.filter((_) => _.length));
                props.onChange?.(values);
              }}
            >
              {options.map((option) => {
                return (
                  <MenuItemOption
                    key={`multiselect-menu-${option}`}
                    type="button"
                    value={option}
                    isChecked={true}
                  >
                    {option}
                  </MenuItemOption>
                );
              })}
            </MenuOptionGroup>
          </MenuList>
        </>
      )}
    </Menu>
  );
};

export default MultiSelectMenu;
