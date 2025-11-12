import { memo, useCallback, useState } from "react";
import CustomNode from "../../../src/nodes/CustomNode";

const CharacterCardNode: CustomNode = ({ data, sendSignal }) => {
  const [isDragOver, setIsDragOver] = useState(false);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback(
    async (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragOver(false);

      const files = Array.from(e.dataTransfer.files);
      const imageFile = files.find((file) => file.type.startsWith("image/"));

      if (imageFile) {
        try {
          // Read the image file as base64
          const base64Data = await readFileAsBase64(imageFile);

          // Send the image data to backend for processing
          sendSignal("image_dropped", base64Data);
        } catch (error) {
          console.error("Error processing image:", error);
        }
      }
    },
    [sendSignal]
  );

  const readFileAsBase64 = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        if (typeof reader.result === "string") {
          resolve(reader.result);
        } else {
          reject(new Error("Failed to read file as base64"));
        }
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  };

  const characterData = data.character_data || {};
  const hasCharacterData = Object.keys(characterData).length > 0;

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "8px",
        padding: "12px",
        minWidth: "200px",
        minHeight: "150px",
      }}
    >
      {/* Drop Zone */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        style={{
          border: `2px dashed ${isDragOver ? "#007bff" : "#ccc"}`,
          borderRadius: "8px",
          padding: "16px",
          textAlign: "center",
          backgroundColor: isDragOver ? "#f8f9fa" : "#fff",
          cursor: "pointer",
          transition: "all 0.2s ease",
          minHeight: "120px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
        title="Drop a character card image here"
      >
        {hasCharacterData ? (
          <div
            style={{
              fontSize: "10px",
              color: "#666",
              marginTop: "4px",
              fontWeight: "bold",
            }}
          >
            {characterData.name || "Character"}
          </div>
        ) : (
          <div>
            <div
              style={{
                fontSize: "14px",
                fontWeight: "bold",
                marginBottom: "4px",
              }}
            >
              Character Card
            </div>
            <div style={{ fontSize: "12px", color: "#666" }}>
              Drop a character card image here
            </div>
          </div>
        )}
      </div>

      {/* Status Indicator */}
      {hasCharacterData && (
        <div
          style={{
            fontSize: "10px",
            color: "#4CAF50",
            textAlign: "center",
            padding: "4px",
            backgroundColor: "#f0f9f0",
            borderRadius: "4px",
          }}
        >
          ✓ Character data extracted
        </div>
      )}
    </div>
  );
};

export default memo(CharacterCardNode);
