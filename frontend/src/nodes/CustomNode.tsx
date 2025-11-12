/* eslint-disable @typescript-eslint/no-explicit-any */
// import { Component, type ReactNode } from "react";

import type { ReactNode } from "react";

export interface CustomNodeProps {
  data: any;
  sync: (data: any) => void;
  sendSignal: (name: string, params: any) => void;
  setSignalCallback: (callback: (signal: string, params: any) => void) => void;
}

export default interface CustomNode {
  (props: CustomNodeProps): ReactNode;
}
