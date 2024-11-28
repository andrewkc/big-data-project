'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { supabase } from '@/lib/supabaseClient';
import { stripIndent, oneLine } from 'common-tags';
import ReactMarkdown from 'react-markdown';

import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent
} from '@/components/ui/card';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
  DropdownMenuLabel
} from '@/components/ui/dropdown-menu';
import {
  PlusIcon,
  ClockIcon,
  SendIcon,
  MicIcon,
  MoreHorizontalIcon,
  DownloadIcon,
  TrashIcon,
  PencilIcon
} from 'lucide-react';

export default function ChatAI() {
  const [inputValue, setInputValue] = useState('');
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);
  const [messages, setMessages] = useState([]);

  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleSendMessage = async () => {
    const searchText = inputValue;

    if (searchText && searchText.trim()) {
      setMessages([...messages, { sender: 'user', text: searchText }]);
      setInputValue('');

      const res = await fetch(
        `${process.env.NEXT_PUBLIC_SUPABASE_URL}/functions/v1/embed`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY}`
          },
          body: JSON.stringify({ prompt: searchText.replace(/\n/g, ' ') })
        }
      );

      if (res.status !== 200) {
        console.log('error fetch');
      } else {
        const data = await res.json();

        const { data: documents } = await supabase
          .rpc('match_documents', {
            query_embedding: data.embedding,
            match_threshold: 0.8
          })
          .select('content')
          .limit(5);

        let contextText = '';
        for (let i = 0; i < documents.length; i++) {
          const document = documents[i];
          const content = document.content;
          contextText += `${content.trim()}\n--\n`;
        }
        /*
          Dime Regulaciones Aduaneras para Enviar y Traer Productos Entre Estados Unidos y China
              */
        const prompt = generatePrompt(contextText, searchText);
        console.log('prompt ', prompt);
        const answer = await generateAnswer(prompt);
        // const answer = "Response "
        setMessages([
          ...messages,
          { sender: 'user', text: searchText },
          { sender: 'ai', text: answer }
        ]);
      }
    }
  };

  const generatePrompt = (contextText: string, searchText: string) => {
    const prompt = stripIndent`${oneLine`
        
      `}
 
        Contexto de las secciones:
        ${contextText}


        Pregunta: """
        ${searchText}
        """
    `;
    return prompt;
  };

  const generateAnswer = async (prompt: string) => {
    const ollamaResponse = await fetch('http://localhost:11434/api/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'llama3.2',
        prompt: prompt,
        stream: true // Mantener el streaming en true
      })
    });

    const reader = ollamaResponse.body.getReader();
    let result = ''; // Inicializa el resultado concatenado
    let done = false;

    // Lee la respuesta mientras no esté terminada
    while (!done) {
      const { done: streamDone, value } = await reader.read();
      done = streamDone;

      if (value) {
        const chunk = new TextDecoder('utf-8').decode(value);

        // Intenta parsear el chunk
        try {
          const chunkJson = JSON.parse(chunk);
          result += chunkJson.response; // Acumula la respuesta

          // Actualiza los mensajes en tiempo real
          setMessages((prev) => [
            ...prev.slice(0, -1), // Mantiene todos menos el último
            { sender: 'ai', text: result } // Agrega la respuesta acumulada
          ]);

          // Si la respuesta está completa
          if (chunkJson.done) {
            done = chunkJson.done;
          }
        } catch (error) {
          console.error('Error parsing chunk:', error);
        }
      }
    }
    return result;
  };

  const handleVoiceInput = () => {
    console.log('Iniciando entrada de voz');
  };

  const toggleHistory = () => {
    setIsHistoryOpen(!isHistoryOpen);
  };

  const chatHistory = [
    {
      date: 'Hoy',
      chats: [
        { title: 'Importación de electrónicos' },
        { title: 'Aranceles para textiles' }
      ]
    },
    {
      date: 'Ayer',
      chats: [
        { title: 'Requisitos fitosanitarios' },
        { title: 'Proceso de desaduanaje' },
        { title: 'Impuestos de importación' }
      ]
    },
    {
      date: 'Hace 2 semanas',
      chats: [
        { title: 'Documentación necesaria' },
        { title: 'Regulaciones aduaneras' }
      ]
    }
  ];

  return (
    <div className="max-h-96 min-h-screen bg-white">
      <header className="flex items-center justify-between border-b p-4 ">
        <div className="flex items-center space-x-4">
          <span className="text-xl font-bold">ImportAI</span>
        </div>
        <div className="flex items-center space-x-4">
          <Button variant="outline" size="sm">
            <PlusIcon className="mr-2 h-4 w-4" />
            Nuevo Chat
          </Button>
          <DropdownMenu open={isHistoryOpen} onOpenChange={setIsHistoryOpen}>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="sm" onClick={toggleHistory}>
                <ClockIcon className="mr-2 h-4 w-4" />
                Historial
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="w-64">
              <div className="p-2">
                <Input placeholder="Buscar un chat..." className="mb-2" />
              </div>
              <DropdownMenuSeparator />
              <div className="max-h-64 overflow-y-auto">
                {chatHistory.map((group, groupIndex) => (
                  <React.Fragment key={groupIndex}>
                    <DropdownMenuLabel>{group.date}</DropdownMenuLabel>
                    {group.chats.map((chat, chatIndex) => (
                      <DropdownMenuItem
                        key={chatIndex}
                        className="flex items-center justify-between"
                      >
                        <span>{chat.title}</span>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="sm">
                              <MoreHorizontalIcon className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent>
                            <DropdownMenuItem>
                              <DownloadIcon className="mr-2 h-4 w-4" />
                              Descargar chat
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <PencilIcon className="mr-2 h-4 w-4" />
                              Renombrar chat
                            </DropdownMenuItem>
                            <DropdownMenuItem className="text-red-600">
                              <TrashIcon className="mr-2 h-4 w-4" />
                              Borrar chat
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </DropdownMenuItem>
                    ))}
                    {groupIndex < chatHistory.length - 1 && (
                      <DropdownMenuSeparator />
                    )}
                  </React.Fragment>
                ))}
              </div>
              <DropdownMenuSeparator />
              <DropdownMenuItem>
                <TrashIcon className="mr-2 h-4 w-4" />
                Vaciar chats
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </header>

      <main className="mx-auto mt-8 h-96 w-full overflow-y-scroll p-4">
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>
              Bienvenido al Asistente de StatsBomb de Estadística  de Fútbol 
            </CardTitle>
            <CardDescription>
            Este chatbot está entrenado con información de StatsBomb sobre estadísticas avanzadas del fútbol, 
            proporcionando datos detallados sobre partidos, jugadores y equipos.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-500">
              Utiliza inteligencia artificial para proporcionar respuestas precisas y actualizadas sobre estadísticas de fútbol, 
              análisis de partidos, rendimiento de jugadores, tácticas y más.
            </p>
          </CardContent>
        </Card>

        <div className="mb-8 grid grid-cols-2 gap-4">
          {[
            {
              title: '¿Cuáles son las estadísticas clave',
              description: 'para analizar el rendimiento de un jugador?'
            },
            {
              title: '¿Cómo se calcula',
              description: 'el Expected Goals (xG) de un jugador?'
            },
            {
              title: 'Explícame el análisis',
              description: 'de un partido de fútbol usando datos de StatsBomb'
            },
            {
              title: '¿Qué métricas se utilizan',
              description: 'para evaluar el desempeño de un equipo?'
            }
          ].map((item, index) => (
            <Card key={index} className="cursor-pointer hover:bg-gray-50">
              <CardHeader>
                <CardTitle className="text-sm font-medium">
                  {item.title}
                </CardTitle>
                <CardDescription className="text-xs">
                  {item.description}
                </CardDescription>
              </CardHeader>
            </Card>
          ))}
        </div>

        <div className="mb-8 space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${
                message.sender === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              <div
                className={`max-w-xs rounded-lg p-5 ${
                  message.sender === 'user'
                    ? 'bg-green-500 text-white'
                    : 'bg-blue-500 text-white'
                }`}
              >
                {message.sender === 'ai' ? (
                  <ReactMarkdown>{message.text}</ReactMarkdown>
                ) : (
                  message.text
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="flex items-center space-x-2">
          <Input
            placeholder="Escribe tu pregunta sobre StatsBomb..."
            className="flex-grow"
            value={inputValue}
            onChange={handleInputChange}
          />
          <Button
            size="icon"
            onClick={handleVoiceInput}
            className="bg-blue-500 text-white hover:bg-blue-600"
          >
            <MicIcon className="h-4 w-4" />
          </Button>
          <Button
            size="icon"
            onClick={handleSendMessage}
            className="bg-green-500 text-white hover:bg-green-600"
          >
            <SendIcon className="h-4 w-4" />
          </Button>
        </div>

        <p className="mt-4 text-center text-xs text-gray-500">
          Asistente de IA.
        </p>
      </main>
    </div>
  );
}