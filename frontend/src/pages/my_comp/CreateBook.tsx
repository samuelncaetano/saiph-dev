import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { PlusCircle } from "lucide-react"

const CreateBook = () => {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="default">
            <PlusCircle className="w-4 h-4 mr-2"/>
            Adicionar livro
            </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-auto">
        <DialogHeader>
          <DialogTitle className="text-center">Adicionar livro</DialogTitle>
          <DialogDescription className="text-center">
            Adicione seu livro aqui. Clique em adicionar quando terminar.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="title" className="text-center">
              Título
            </Label>
            <Input
              id="title"
              className="col-span-3"
            />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="author" className="text-center">
              Autor
            </Label>
            <Input
              id="author"
              className="col-span-3"
            />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="date" className="text-center" typeof="number">
              Ano de publicação
            </Label>
            <Input
              id="date"
              className="col-span-3"
            />
          </div>
        </div>
        <DialogFooter>
            <DialogClose asChild>
                <Button variant="outline">Cancelar</Button>
            </DialogClose>
            <Button type="submit">Adicionar</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}

export default CreateBook