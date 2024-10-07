import { ColumnDef } from "@tanstack/react-table"

export type Process = {
  pid: string
  name: string
  status: string
  cpu_usage: string
  memory_usage: string
}

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
    header: "CPU Usage",
    accessorFn: (row) => `${row.cpu_usage}%`,
  },
  {
    accessorKey: "memory_usage",
    header: "Memory Usage",
  },
]
