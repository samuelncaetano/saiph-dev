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
          title: "Login success",
          description: "You were authenticated with success.",
        });
  
        // Redireciona para o dashboard
        navigate("/dashboard");
      } catch (error) {
        toast({
          title: "Login error",
          description:
            "There ocurred an error when trying to login. Please, try again.",
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
          title: "Sign-up success",
          description: "Your account was created with success.",
        })
        // Aqui você pode automaticamente fazer login do usuário, redirecionar, etc.
        console.log("Registration successful", response.data)
      } catch (error) {
        toast({
          title: "Sign-up error",
          description: "There ocurred an error when trying to create your account. Please, try again.",
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
            <CardTitle>Welcome</CardTitle>
            <CardDescription>Sign in or create a new account</CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="login" className="w-full">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="login">Login</TabsTrigger>
                <TabsTrigger value="register">Sign up</TabsTrigger>
              </TabsList>
              <TabsContent value="login">
                <form onSubmit={handleLogin}>
                  <div className="grid w-full items-center gap-4">
                    <div className="flex flex-col space-y-1.5">
                      <Label htmlFor="login-email">E-mail</Label>
                      <Input
                        id="login-email"
                        name="login-email"
                        type="email"
                        placeholder="your@email.com"
                        required
                      />
                    </div>
                    <div className="flex flex-col space-y-1.5">
                      <Label htmlFor="login-password">Password</Label>
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
                    {isLoading ? "Logging in..." : "Login"}
                  </Button>
                </form>
              </TabsContent>
              <TabsContent value="register">
                <form onSubmit={handleRegister}>
                  <div className="grid w-full items-center gap-4">
                    <div className="flex flex-col space-y-1.5">
                      <Label htmlFor="register-name">Name</Label>
                      <Input id="register-name" name="register-name" placeholder="your name" required />
                    </div>
                    <div className="flex flex-col space-y-1.5">
                      <Label htmlFor="register-email">E-mail</Label>
                      <Input id="register-email" name="register-email" type="email" placeholder="your@email.com" required />
                    </div>
                    <div className="flex flex-col space-y-1.5">
                      <Label htmlFor="register-password">Password</Label>
                      <Input id="register-password" name="register-password" type="password" required />
                    </div>
                    <div className="flex flex-col space-y-1.5">
                      <Label htmlFor="register-password">Age</Label>
                      <Input id="register-age" name="register-age" type="age" required />
                    </div>
                  </div>
                  <Button className="w-full mt-6" type="submit" disabled={isLoading}>
                    {isLoading ? "Signing in..." : "Sign in"}
                  </Button>
                </form>
              </TabsContent>
            </Tabs>
          </CardContent>
          <CardFooter className="flex justify-center">
            <p className="text-sm text-gray-500">
              By continuing, you agree to our Terms of Service and Privacy Policy.
            </p>
          </CardFooter>
        </Card>
      </div>
    )
  }