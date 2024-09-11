import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { BookType, IdCard, Calendar, Trash2, PencilLine} from "lucide-react"

const BookCard = () => {
    return (
        <Card>
            <CardContent>
                <div className="grid gap-4 pt-8 pb-4">                            
                    <p className="flex justify-center gap-x-6">
                        <BookType className=""/>
                        Título
                    </p>
                </div>
                <div className="grid gap-4 py-4">
                    <p className="flex justify-center gap-x-6">
                        <IdCard className=""/>
                        Autor
                    </p>
                </div>
                <div className="grid gap-4 py-4">
                    <p className="flex justify-center gap-x-6">
                        <Calendar className=""/>
                        Ano de publicação
                    </p>
                </div>
            </CardContent>
            <CardFooter className="flex justify-center gap-x-6">
                <Button variant="destructive">
                    <Trash2 className="w-4 h-4 mr-2" />
                    Deletar
                </Button>
                <Button variant="outline">
                    <PencilLine className="w-4 h-4 mr-2" />
                    Editar
                </Button>
            </CardFooter>
        </Card>
    )
}

export default BookCard