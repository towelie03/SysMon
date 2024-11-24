import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { z } from "zod";
import { ThemeContext } from "@/theme_provider";
import { useContext, useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { SettingsDataContext } from "./settings_provider";

const formSchema = z.object({
  cpu_threshold: z.coerce.number().min(0).max(100).default(80),
  memory_threshold: z.coerce.number().min(0).max(100).default(80),
  disk_threshold: z.coerce.number().min(0).max(100).default(80),
  network_threshold: z.coerce.number().min(0).max(10000000).default(1000000),
  gpu_threshold: z.coerce.number().min(0).max(100).default(80),
  check_interval: z.coerce.number().min(0).max(100).default(10),
});

export function SettingsView() {
  const theme = useContext(ThemeContext);
  const settings = useContext(SettingsDataContext)

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    shouldUseNativeValidation: true,
    defaultValues: {
      cpu_threshold: settings.cpu_threshold,
      memory_threshold: settings.memory_threshold,
      disk_threshold: settings.disk_threshold,
      network_threshold: settings.network_threshold,
      gpu_threshold: settings.gpu_threshold,
      check_interval: settings.check_interval,
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values);
    var res = await fetch("http://localhost:8000/settings", {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        theme: theme.theme,
        ...values,
      }),
    });

    if (res.ok) {
      toast("Settings updated succesfully!")
    } else {
      toast("Something went wrong...")
    }
  }

  return (
    <div className="flex flex-col gap-8 w-full h-full">
      <div className="flex flex-col gap-4">
        <div className="text-4xl font-bold">Theme</div>
        <div>
          <Select
            onValueChange={(value) => {
              theme.setTheme(value);
            }}
          >
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder={theme.theme} />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="Catpuccin">Catpuccin</SelectItem>
              <SelectItem value="DefaultGreen">Default Green</SelectItem>
              <SelectItem value="DarkRed">Dark Red</SelectItem>
              <SelectItem value="LightRed">Light Red</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        <div className="text-4xl font-bold">Notification Service</div>
        <Card>
          <CardHeader>
            <CardTitle>Notification Service Settings</CardTitle>
            <CardDescription>
              Customize the thresholds for the notifications
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Form {...form}>
              <form
                onSubmit={form.handleSubmit(onSubmit)}
                className="space-y-8"
              >
                <div className="flex flex-wrap gap-6">
                  <FormField
                    control={form.control}
                    name="cpu_threshold"
                    render={({ field }) => (
                      <FormItem className="w-1/3">
                        <FormLabel>CPU Threshold</FormLabel>
                        <FormControl>
                          <Input type="number" min={0} max={100} {...field} />
                        </FormControl>
                        <FormDescription>
                          The CPU usage % to notify at
                        </FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="memory_threshold"
                    render={({ field }) => (
                      <FormItem className="w-1/3">
                        <FormLabel>Memory Threshold</FormLabel>
                        <FormControl>
                          <Input type="number" min={0} max={100} {...field} />
                        </FormControl>
                        <FormDescription>
                          The CPU usage % to notify at
                        </FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="disk_threshold"
                    render={({ field }) => (
                      <FormItem className="w-1/3">
                        <FormLabel>Disk Threshold</FormLabel>
                        <FormControl>
                          <Input type="number" min={0} max={100} {...field} />
                        </FormControl>
                        <FormDescription>
                          The Disk usage % to notify at
                        </FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="network_threshold"
                    render={({ field }) => (
                      <FormItem className="w-1/3">
                        <FormLabel>Network Threshold</FormLabel>
                        <FormControl>
                          <Input
                            type="number"
                            min={0}
                            max={1000000}
                            {...field}
                          />
                        </FormControl>
                        <FormDescription>
                          The Network usage % to notify at
                        </FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="check_interval"
                    render={({ field }) => (
                      <FormItem className="w-1/3">
                        <FormLabel>Check Interval</FormLabel>
                        <FormControl>
                          <Input type="number" min={0} max={100} {...field} />
                        </FormControl>
                        <FormDescription>
                          How often to check (in seconds)
                        </FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
                <Button type="submit">Submit</Button>
              </form>
            </Form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
