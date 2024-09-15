import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
  } from "@/components/ui/dialog";
  import { Edit, Plus, Trash2, BookType } from "lucide-react";
  import React, { useEffect, useState } from "react";
  import { Button } from "@/components/ui/button";
  import { Input } from "@/components/ui/input";
  import { Label } from "@/components/ui/label";
  import UserProfile from "./UserProfile";
  import axios from "axios";
  import { useToast } from "@/hooks/use-toast";
  import { withAuth } from "./withAuth"; 
  import { Card, CardContent, CardFooter } from "@/components/ui/card";
  
  interface Book {
    id: string;
    title: string;
    is_read: boolean;
  }
  
  const API_BASE_URL = "http://localhost:8080";
  
  function BookDashboard() {
    const [books, setBooks] = useState<Book[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [editingBook, setEditingBook] = useState<Book | null>(null);
    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const { toast } = useToast();
  
    const userId = localStorage.getItem("user_id");
  
    useEffect(() => {
      if (userId) {
        fetchBooks();
      } else {
        toast({
          title: "Error",
          description: "User not authenticated.",
          variant: "destructive",
        });
      }
    }, [userId]);
  
    const fetchBooks = async () => {
      setIsLoading(true);
      try {
        const response = await axios.get(`${API_BASE_URL}/books/user/${userId}`);
  
  
        if (response.data && Array.isArray(response.data)) {
          setBooks(response.data);  // Define os livros com o status atual
        } else {
          throw new Error("Invalid data format received from the API");
        }
  
  
      } catch (error) {
        toast({
          title: "Error",
          description: "Failed to fetch books. Please try again.",
          variant: "destructive",
        });
      } finally {
        setIsLoading(false);
      }
    };
  
    const toggleReadStatus = async (id: string) => {
      try {
        await axios.patch(`${API_BASE_URL}/books/toggle-status/${id}`, {});
        const updatedBooks = books.map((book) =>
          book.id === id ? { ...book, is_read: !book.is_read } : book
        );
        setBooks(updatedBooks);
        toast({
          title: "Success",
          description: "Book status updated successfully.",
        });
      } catch (error) {
        toast({
          title: "Error",
          description: "Failed to update book status. Please try again.",
          variant: "destructive",
        });
      }
    };
  
    const deleteBook = async (id: string) => {
      try {
        await axios.delete(`${API_BASE_URL}/books/${id}`);
        setBooks(books.filter((book) => book.id.toString() !== id.toString()));
        toast({
          title: "Success",
          description: "Book deleted successfully.",
        });
      } catch (error) {
        toast({
          title: "Error",
          description: "Failed to delete book. Please try again.",
          variant: "destructive",
        });
      }
    };
  
    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
      event.preventDefault();
      const formData = new FormData(event.currentTarget);
  
      const bookData = {
        title: formData.get("title") as string,
        user_id: Number(userId),
      };
  
      try {
        if (editingBook) {
          const response = await axios.patch(
            `${API_BASE_URL}/books/${editingBook.id}`,
            bookData
          );
          setBooks(
            books.map((book) =>
              book.id === editingBook.id ? response.data : book
            )
          );
          toast({
            title: "Success",
            description: "Book updated successfully.",
          });
        } else {
          const response = await axios.post(`${API_BASE_URL}/books`, bookData);
          setBooks([...books, response.data]);
          toast({
            title: "Success",
            description: "Book added successfully.",
          });
        }
        setEditingBook(null);
        setIsDialogOpen(false);
      } catch (error) {
        toast({
          title: "Error",
          description: `Failed to ${
            editingBook ? "update" : "add"
          } book. Please try again.`,
          variant: "destructive",
        });
      }
    };
  
    return (
      <div className="container mx-auto p-4">
        <div className="flex justify-end mb-4">
          <UserProfile />
        </div>
        <h1 className="text-2xl font-bold mb-4">
          Your Book Management Dashboard
        </h1>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button className="mb-4" onClick={() => setEditingBook(null)}>
              <Plus className="mr-2 h-4 w-4" /> Add New Book
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>
                {editingBook ? "Edit Book" : "Add New Book"}
              </DialogTitle>
              <DialogDescription>
                {editingBook
                  ? "Make changes to your book here."
                  : "Enter the details of your new book here."}
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={handleSubmit}>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="title" className="text-right">
                    Title
                  </Label>
                  <Input
                    id="title"
                    name="title"
                    defaultValue={editingBook?.title}
                    className="col-span-3"
                    required
                    aria-required="true"
                  />
                </div>
              </div>
              <Button type="submit">Save</Button>
            </form>
          </DialogContent>
        </Dialog>
        {isLoading ? (
                <Card>
                    <CardContent>
                    <div className="grid gap-4 pt-8 pb-4">
                        <p className="text-center">Loading...</p>
                    </div>
                    </CardContent>
                </Card>
                ) : books.length === 0 ? (
                <Card>
                    <CardContent>
                    <div className="grid gap-4 pt-8 pb-4">
                        <p className="text-center">No books found. Add some books to get started!</p>
                    </div>
                    </CardContent>
                </Card>
                ) : (
                books.map((book) => (
                    <Card key={book.id}>
                    <CardContent>
                        <div className="grid gap-4 pt-8 pb-4">
                        <p className="flex justify-center gap-x-6">
                            <BookType className=""/>
                            {book.title}
                        </p>
                        </div>
                    </CardContent>
                    <CardFooter className="flex justify-center gap-x-6">
                        <Button variant={book.is_read ? "default" : "outline"} onClick={() => toggleReadStatus(book.id)}>
                        {book.is_read ? "Read" : "Unread"}
                        </Button>
                        <Button variant="outline" size="default" onClick={() => { setEditingBook(book); setIsDialogOpen(true); }}>
                        <Edit className="w-4 h-4 mr-2" />
                        Edit
                        </Button>
                        <Button variant="destructive" size="default" onClick={() => deleteBook(book.id)}>
                        <Trash2 className="w-4 h-4 mr-2" />
                        Delete
                        </Button>
                    </CardFooter>
                    </Card>
                ))
            )}
      </div>
    );
  }
  
  export default withAuth(BookDashboard);