import { useReactFlow } from "@xyflow/react";
import { useCallback } from "react";
import {
  ControlledMenu,
  Menu,
  MenuButton,
  MenuItem as MenuItemInner,
  SubMenu as SubMenuInner,
} from "@szhsin/react-menu";

import styles from "./style.module.css";

const menuClassName = ({ state }) =>
  state === "opening"
    ? styles.menuOpening
    : state === "closing"
    ? styles.menuClosing
    : styles.menu;

const menuItemClassName = ({ hover, disabled }) =>
  disabled
    ? styles.menuItemDisabled
    : hover
    ? styles.menuItemHover
    : styles.menuItem;

const submenuItemClassName = (modifiers) =>
  `${styles.submenuItem} ${menuItemClassName(modifiers)}`;

const MenuItem = (props) => (
  <MenuItemInner {...props} className={menuItemClassName} />
);

const SubMenu = (props) => (
  <SubMenuInner
    {...props}
    menuClassName={menuClassName}
    itemProps={{ className: submenuItemClassName }}
    offsetY={-7}
  />
);

/* eslint-disable @typescript-eslint/no-explicit-any */
type PaneContextMenuProps = {
  anchorPoint: { x: number; y: number };
  isOpen: boolean;
  style?: React.CSSProperties;
  createNode: (id: string) => void;
};

export default function PaneContextMenu(props: PaneContextMenuProps) {
  const { anchorPoint, isOpen, style, createNode, ...restProps } = props;

  // return (
  //   <div style={style} className="context-menu" {...restProps}>
  //     <p style={{ margin: "0.5em" }}>
  //       <small>Create Node</small>
  //     </p>
  //     <button onClick={deleteNode}>delete</button>
  //   </div>
  // );

  return (
    <ControlledMenu
      className="menu"
      anchorPoint={anchorPoint}
      state={isOpen ? "open" : "closed"}
      direction="right"
    >
      <MenuItem className="menuItem" onClick={() => console.log("CUT!")}>
        Cut
      </MenuItem>
    </ControlledMenu>
  );
}
