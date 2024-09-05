import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useToast } from "@/hooks/use-toast";

const API_BASE_URL = "http://localhost:8080";

export default function AuthScreenWithAPI() {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const { toast } = useToast();
  const navigate = useNavigate(); // Hook para navegação

  useEffect(() => {
    const user = localStorage.getItem('user');
    if (user) {
      navigate('/dashboard');
    }
  }, [navigate]);

  const handleLogin = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsLoading(true);

    const formData = new FormData(event.currentTarget);
    const email = formData.get("login-email") as string;
    const password = formData.get("login-password") as string;

    try {
      const response = await axios.post(`${API_BASE_URL}/users/login`, {
        email,
        password,
      });
      console.log(response)
      // Salva o nome do usuário no localStorage
      localStorage.setItem('user', response.data);
      localStorage.setItem('user_id', response.data.id);

      toast({
        title: "Login bem-sucedido",
        description: "Você foi autenticado com sucesso.",
      });

      // Redireciona para o dashboard
      navigate("/dashboard");
    } catch (error) {
      toast({
        title: "Erro no login",
        description:
          "Ocorreu um erro ao tentar fazer login. Por favor, tente novamente.",
        variant: "destructive",
      });
      console.error("Login error", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegister = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setIsLoading(true)

    const formData = new FormData(event.currentTarget)
    const name = formData.get("register-name") as string
    const email = formData.get("register-email") as string
    const password = formData.get("register-password") as string
    const age = formData.get("register-age") as unknown

    try {
      const response = await axios.post(`${API_BASE_URL}/users`,
        {
          name,
          email,
          password,
          age
        }
      )
      toast({
        title: "Registro bem-sucedido",
        description: "Sua conta foi criada com sucesso.",
      })
      // Aqui você pode automaticamente fazer login do usuário, redirecionar, etc.
      console.log("Registration successful", response.data)
    } catch (error) {
      toast({
        title: "Erro no registro",
        description: "Ocorreu um erro ao tentar criar sua conta. Por favor, tente novamente.",
        variant: "destructive",
      })
      console.error("Registration error", error)
    } finally {
      setIsLoading(false)
    }
  }


  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <Card className="w-[350px]">
        <CardHeader>
          <CardTitle>Bem-vindo</CardTitle>
          <CardDescription>Faça login ou crie uma nova conta</CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="login" className="w-full">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="login">Login</TabsTrigger>
              <TabsTrigger value="register">Registro</TabsTrigger>
            </TabsList>
            <TabsContent value="login">
              <form onSubmit={handleLogin}>
                <div className="grid w-full items-center gap-4">
                  <div className="flex flex-col space-y-1.5">
                    <Label htmlFor="login-email">Email</Label>
                    <Input
                      id="login-email"
                      name="login-email"
                      type="email"
                      placeholder="seu@email.com"
                      required
                    />
                  </div>
                  <div className="flex flex-col space-y-1.5">
                    <Label htmlFor="login-password">Senha</Label>
                    <Input
                      id="login-password"
                      name="login-password"
                      type="password"
                      required
                    />
                  </div>
                </div>
                <Button
                  className="w-full mt-6"
                  type="submit"
                  disabled={isLoading}
                >
                  {isLoading ? "Entrando..." : "Entrar"}
                </Button>
              </form>
            </TabsContent>
            <TabsContent value="register">
              <form onSubmit={handleRegister}>
                <div className="grid w-full items-center gap-4">
                  <div className="flex flex-col space-y-1.5">
                    <Label htmlFor="register-name">Nome</Label>
                    <Input id="register-name" name="register-name" placeholder="Seu nome" required />
                  </div>
                  <div className="flex flex-col space-y-1.5">
                    <Label htmlFor="register-email">Email</Label>
                    <Input id="register-email" name="register-email" type="email" placeholder="seu@email.com" required />
                  </div>
                  <div className="flex flex-col space-y-1.5">
                    <Label htmlFor="register-password">Senha</Label>
                    <Input id="register-password" name="register-password" type="password" required />
                  </div>
                  <div className="flex flex-col space-y-1.5">
                    <Label htmlFor="register-password">Idade</Label>
                    <Input id="register-age" name="register-age" type="age" required />
                  </div>
                </div>
                <Button className="w-full mt-6" type="submit" disabled={isLoading}>
                  {isLoading ? "Registrando..." : "Registrar"}
                </Button>
              </form>
            </TabsContent>
          </Tabs>
        </CardContent>
        <CardFooter className="flex justify-center">
          <p className="text-sm text-gray-500">
            Ao continuar, você concorda com nossos Termos de Serviço e Política de Privacidade.
          </p>
        </CardFooter>
      </Card>
    </div>
  )
}
