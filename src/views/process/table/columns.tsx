import { Button } from "@/components/ui/button"
import { ColumnDef } from "@tanstack/react-table"
import { ArrowUpDown } from "lucide-react"

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
        )
      },

  },
  {
    accessorKey: "memory_usage",
    header: "Memory Usage",
  },
]
