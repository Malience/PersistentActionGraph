import { memo } from "react";
import CustomNode from "../../../src/nodes/CustomNode";
import TextComponent from "../../../src/components/TextComponent";
import PropertiesComponent from "../../../src/components/PropertiesComponent";

// interface JSONSchema {
//   type: string;
//   name?: string;
//   description?: string;
//   properties?: Record<string, unknown>;
//   required?: string[];
// }

const JSONSchemaNode: CustomNode = ({ data, sync }) => {
  // const [isValidSchema, setIsValidSchema] = useState(true);
  const isValidSchema = true;

  // Build and validate schema whenever inputs change
  // const onUpdate = useCallback(() => {
  //   const buildAndValidateSchema = () => {
  //     try {
  //       // At some point any of this wil matter, but not today
  //       const schema: JSONSchema = {
  //         title: data.title,
  //         description: data.description,
  //         type: "object",
  //       };

  //       // Build properties from the properties data field
  //       // if (data.properties) {
  //       //   try {
  //       //     const properties = JSON.parse(data.properties);
  //       //     if (Array.isArray(properties)) {
  //       //       const validProperties: Record<string, unknown> = {};
  //       //       properties.forEach((prop: any) => {
  //       //         if (prop.title && prop.type) {
  //       //           const propSchema: Record<string, unknown> = {
  //       //             type: prop.type,
  //       //           };

  //       //           if (prop.description)
  //       //             propSchema.description = prop.description;

  //       //           // Add custom options if valid JSON
  //       //           if (prop.custom) {
  //       //             try {
  //       //               const customOptions = JSON.parse(prop.custom);
  //       //               Object.assign(propSchema, customOptions);
  //       //             } catch {
  //       //               // Ignore invalid custom options
  //       //             }
  //       //           }

  //       //           validProperties[prop.title] = propSchema;
  //       //         }
  //       //       });

  //       //       if (Object.keys(validProperties).length > 0) {
  //       //         schema.properties = validProperties;
  //       //       }
  //       //     }
  //       //   } catch {
  //       //     // Ignore invalid properties JSON
  //       //   }
  //       // }

  //       // Add required fields
  //       const requiredList = data.required
  //         .split(",")
  //         .map((field: any) => field.trim())
  //         .filter((field: any) => field);
  //       if (requiredList.length > 0) {
  //         schema.required = requiredList;
  //       }

  //       // Validate the schema structure
  //       const schemaString = JSON.stringify(schema, null, 2);
  //       JSON.parse(schemaString);

  //       console.log(schemaString);

  //       // sync({ ...data, schema: schemaString });
  //       setIsValidSchema(true);
  //     } catch {
  //       // sync({ ...data, schema: null });
  //       setIsValidSchema(false);
  //     }
  //   };

  //   buildAndValidateSchema();
  // }, [data]);

  // const syncFunction = useCallback(
  //   (data: any) => {
  //     sync(data);
  //     onUpdate();
  //   },
  //   [onUpdate, sync]
  // );

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "8px",
        padding: "8px",
        minWidth: "300px",
      }}
    >
      {/* Schema Validation Status */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "8px",
          marginBottom: "4px",
        }}
      >
        <span style={{ fontSize: "12px", fontWeight: "bold" }}>
          Schema Valid:
        </span>
        <div
          style={{
            width: "12px",
            height: "12px",
            borderRadius: "50%",
            backgroundColor: isValidSchema ? "#4CAF50" : "#F44336",
            border: "1px solid #ccc",
            flexShrink: 0,
          }}
          title={isValidSchema ? "Valid JSON Schema" : "Invalid JSON Schema"}
        />
        <span
          style={{
            fontSize: "10px",
            color: isValidSchema ? "#4CAF50" : "#F44336",
          }}
        >
          {isValidSchema ? "Valid" : "Invalid"}
        </span>
      </div>

      {/* Schema Name */}
      <TextComponent
        data={data}
        sync={sync}
        dataField="name"
        label="Schema Name"
        multiline={false}
        placeholder="Enter schema name..."
      />

      {/* Schema Description */}
      <TextComponent
        data={data}
        sync={sync}
        dataField="description"
        label="Schema Description"
        multiline={false}
        placeholder="Enter schema description..."
      />

      {/* Required Fields */}
      <TextComponent
        data={data}
        sync={sync}
        dataField="required"
        label="Required Fields (comma-separated)"
        multiline={false}
        placeholder="field1, field2, field3"
      />

      {/* Properties Component */}
      <PropertiesComponent data={data} sync={sync} dataField="properties" />
    </div>
  );
};

export default memo(JSONSchemaNode);
