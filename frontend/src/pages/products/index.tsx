import { Container } from "../../components/container";
import { Input } from "../../components/input";
import { useForm } from 'react-hook-form'
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod'
import { api_cart } from "../../services/api_cart";
import toast from "react-hot-toast";
import { Link } from "react-router-dom";

const schema = z.object({
    name: z.string().nonempty("O campo nome do produto é obrigatório"),
    title: z.string().nonempty("O título do produto é obrigatório"),
    description: z.string().optional(),
    price: z.coerce.number().positive("O preço deve ser um valor positivo"),
    stock: z.coerce.number().int().nonnegative("O estoque deve ser um número inteiro não negativo"),
    cover: z.string().url("A URL da imagem do produto é inválida"),
})

type FormData = z.infer<typeof schema>

export function Products(){
    const {
        register,
        handleSubmit,
        reset,
        formState: { errors }
    } = useForm<FormData>({
        resolver: zodResolver(schema),
        mode: "onChange"
    })

    async function onSubmit(data: FormData) {
        const token = localStorage.getItem("@token");
        if (!token) {
            console.error("Usuário não autenticado");
            return;
        }

        try {
            const response = await api_cart.post("/products/", data, {
                headers: {
                    Authorization: `Token ${token}`,
                },
            });

            console.log("Produto cadastrado com sucesso", response.data);
            toast.success("Produto cadastrado com sucesso!")
            reset()
        } catch (error) {
            console.error("Erro ao cadastrar produto", error);
            toast.error('Apenas administradores podem cadastrar produtos', {
                style: {
                    borderRadius: 10,
                    backgroundColor: '#FF0000',
                    color: '#FFF',
                    },
            })
        }
    }


    return(
        <Container>
            <h1 className="font-bold text-2xl mb-6 mt-10 text-center">Cadastro de Produtos</h1>

            <div className="flex justify-center items-center flex-col gap-4">
                <form
                className="bg-white max-w-xl w-full rounded-lg p-4"
                onSubmit={handleSubmit(onSubmit)}
                >

                   {/* Nome do Produto */}
                    <div className="mb-3">
                        <label className="block font-medium text-gray-700 mb-1">Nome do Produto</label>
                        <Input type="text" placeholder="Digite o nome do produto" name="name"  error={errors.name?.message} register={register} />
                    </div>

                    {/* Título */}
                    <div className="mb-3">
                        <label className="block font-medium text-gray-700 mb-1">Título do produto</label>
                        <Input type="text" placeholder="Digite o título do produto" name="title" error={errors.title?.message} register={register} />
                    </div>

                    {/* Descrição */}
                    <div className="mb-3">
                        <label className="block font-medium text-gray-700 mb-1">Descrição</label>
                        <textarea className="w-full border rounded-md p-2" placeholder="Digite a descrição" {...register("description")} />
                        {errors.description && <p className="text-red-500 text-sm mt-1">{errors.description.message}</p>}
                    </div>

                    {/* Preço */}
                    <div className="mb-3">
                        <label className="block font-medium text-gray-700 mb-1">Preço (R$)</label>
                        <Input type="number" step="0.01" placeholder="Digite o preço" name="price" error={errors.price?.message} register={register} />
                    </div>

                    {/* Estoque */}
                    <div className="mb-3">
                        <label className="block font-medium text-gray-700 mb-1">Estoque</label>
                        <Input type="number" placeholder="Digite a quantidade em estoque" name="stock" error={errors.stock?.message} register={register} />
                    </div>

                    {/* URL da Imagem */}
                    <div className="mb-3">
                        <label className="block font-medium text-gray-700 mb-1">URL da Imagem</label>
                        <Input type="text" placeholder="Digite a URL da imagem" name='cover' error={errors.cover?.message} register={register} />
                    </div>

                    <button type="submit" className="bg-zinc-900 w-full rounded-md text-white h-10 font-medium hover:bg-zinc-800 transition">
                        Cadastrar
                    </button>

                    <div className="mt-3 text-center">
                        <Link className="relative" to="/">
                            <span className="text-blue-600 font-medium hover:underline hover:text-blue-800 transition duration-200">
                                Voltar para Home
                            </span>
                        
                        </Link>
                    </div>

                </form>
            </div>
        </Container>
    )
}