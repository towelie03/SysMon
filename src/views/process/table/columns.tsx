import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { kill_process } from "@/controllers/process_controller";
import { ColumnDef } from "@tanstack/react-table";
import { ArrowUpDown, MoreHorizontal } from "lucide-react";

export type Process = {
  pid: string;
  name: string;
  status: string;
  cpu_usage: string;
  memory_usage: string;
};

export const columns: ColumnDef<Process>[] = [
  {
    accessorKey: "pid",
    header: "Pid",
  },
  {
    accessorKey: "name",
    header: "Name",
  },
  {
    accessorKey: "status",
    header: "Status",
  },
  {
    accessorKey: "cpu_usage",
    accessorFn: (row) => `${row.cpu_usage}%`,
    cell: (props) => <span className="pl-4">{props.getValue() as string}</span>,
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          CPU Usage
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      );
    },
  },
  {
    accessorKey: "memory_usage",
    header: "Memory Usage",
  },
  {
    id: "actions",
    enableHiding: false,
    cell: ({ row }) => {
      const process = row.original;

      return (
        <div className="dark">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="h-8 w-8 p-0">
                <span className="sr-only">Open menu</span>
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>Actions</DropdownMenuLabel>
              <DropdownMenuItem
                onClick={() => {
                  kill_process(Number(process.pid)).then(() => {
                    console.log("process killed")
                  });
                }}
              >
                Kill Process
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      );
    },
  },
];
