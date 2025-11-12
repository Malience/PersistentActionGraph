/* eslint-disable @typescript-eslint/no-explicit-any */
import { memo, useCallback, useEffect } from "react";
import CustomNode from "../../../src/nodes/CustomNode";

const ConsoleNode: CustomNode = ({ setSignalCallback }) => {
  const onSignal = useCallback((signal: string, params: any) => {
    if (signal === "console") {
      console.log(params);
    }
  }, []);

  useEffect(() => {
    setSignalCallback(onSignal);
  }, [onSignal, setSignalCallback]);

  return <></>;
};

export default memo(ConsoleNode);
