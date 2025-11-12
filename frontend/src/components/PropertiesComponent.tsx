/* eslint-disable @typescript-eslint/no-explicit-any */
import { memo, useState, useEffect } from "react";
import TextComponent from "./TextComponent";
import DropdownComponent from "./DropdownComponent";

export interface Property {
  id: string;
  name: string;
  description: string;
  type: string;
  custom: string;
}

export interface PropertiesComponentProps {
  data: any;
  sync: (data: any) => void;
  dataField: string;
}

const propertyTypes = [
  { value: "string", label: "String" },
  { value: "number", label: "Number" },
  { value: "integer", label: "Integer" },
  { value: "boolean", label: "Boolean" },
  { value: "array", label: "Array" },
  { value: "object", label: "Object" },
  { value: "null", label: "Null" },
];

const PropertiesComponent: React.FC<PropertiesComponentProps> = ({
  data,
  sync,
  dataField,
}) => {
  const [properties, setProperties] = useState<Property[]>([]);

  // Initialize properties from data
  useEffect(() => {
    if (data[dataField]) {
      try {
        const parsedProperties = JSON.parse(data[dataField]);
        if (Array.isArray(parsedProperties)) {
          setProperties(parsedProperties);
        }
      } catch {
        setProperties([]);
      }
    } else {
      setProperties([]);
    }
  }, [data, dataField]);

  // Sync properties array to data
  const syncProperties = (newProperties: Property[]) => {
    setProperties(newProperties);
    sync({
      ...data,
      [dataField]: JSON.stringify(newProperties),
    });
  };

  // Add a new property
  const addProperty = () => {
    const newProperty: Property = {
      id: Date.now().toString(),
      name: "",
      description: "",
      type: "string",
      custom: "",
    };
    syncProperties([...properties, newProperty]);
  };

  // Remove a property
  const removeProperty = (id: string) => {
    syncProperties(properties.filter((prop) => prop.id !== id));
  };

  // Update a property field
  const updateProperty = (id: string, field: keyof Property, value: string) => {
    const updatedProperties = properties.map((prop) =>
      prop.id === id ? { ...prop, [field]: value } : prop
    );
    syncProperties(updatedProperties);
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
      {/* Properties Section Header */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          marginBottom: "8px",
        }}
      >
        <span style={{ fontSize: "12px", fontWeight: "bold" }}>
          Properties:
        </span>
        <button
          onClick={addProperty}
          style={{
            padding: "2px 8px",
            fontSize: "12px",
            backgroundColor: "#4CAF50",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          +
        </button>
      </div>

      {/* Properties List */}
      {properties.map((property, index) => (
        <div
          key={property.id}
          style={{
            border: "1px solid #ddd",
            borderRadius: "4px",
            padding: "8px",
            marginBottom: "8px",
            backgroundColor: "#f9f9f9",
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              marginBottom: "6px",
            }}
          >
            <span style={{ fontSize: "11px", fontWeight: "bold" }}>
              Property {index + 1}
            </span>
            <button
              onClick={() => removeProperty(property.id)}
              style={{
                padding: "1px 6px",
                fontSize: "10px",
                backgroundColor: "#F44336",
                color: "white",
                border: "none",
                borderRadius: "3px",
                cursor: "pointer",
              }}
            >
              -
            </button>
          </div>

          {/* Property Title */}
          <TextComponent
            data={{ value: property.name }}
            sync={(newData) =>
              updateProperty(property.id, "name", newData.value)
            }
            dataField="value"
            label="Name"
            multiline={false}
            placeholder="Property name..."
          />

          {/* Property Type Dropdown */}
          <DropdownComponent
            data={{ value: property.type }}
            sync={(newData) =>
              updateProperty(property.id, "type", newData.value)
            }
            dataField="value"
            label="Type"
            options={propertyTypes}
          />

          {/* Property Description */}
          <TextComponent
            data={{ value: property.description }}
            sync={(newData) =>
              updateProperty(property.id, "description", newData.value)
            }
            dataField="value"
            label="Description"
            multiline={false}
            placeholder="Property description..."
          />

          {/* Custom Options */}
          <TextComponent
            data={{ value: property.custom }}
            sync={(newData) =>
              updateProperty(property.id, "custom", newData.value)
            }
            dataField="value"
            label="Custom (JSON)"
            multiline={true}
            rows={2}
            placeholder='{"format": "email", "minLength": 5}'
          />
        </div>
      ))}
    </div>
  );
};

export default memo(PropertiesComponent);
