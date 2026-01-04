import React, { useState } from 'react';

interface FormField {
  name: string;
  label: string;
  type: 'text' | 'email' | 'number' | 'select' | 'textarea';
  required?: boolean;
  options?: Array<{ value: string; label: string }>;
}

interface FormBuilderProps {
  fields: FormField[];
  onSubmit: (data: Record<string, any>) => void;
  submitText?: string;
}

export default function FormBuilder({ fields, onSubmit, submitText = 'Submit' }: FormBuilderProps) {
  const [formData, setFormData] = useState<Record<string, any>>({});
  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleChange = (e: React.ChangeEvent<any>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: Record<string, string> = {};

    fields.forEach(field => {
      if (field.required && !formData[field.name]) {
        newErrors[field.name] = `${field.label} is required`;
      }
    });

    if (Object.keys(newErrors).length === 0) {
      onSubmit(formData);
    } else {
      setErrors(newErrors);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {fields.map(field => (
        <div key={field.name}>
          <label className="block text-sm font-medium mb-1">{field.label}</label>
          {field.type === 'textarea' ? (
            <textarea
              name={field.name}
              value={formData[field.name] || ''}
              onChange={handleChange}
              className="w-full border rounded p-2"
              required={field.required}
            />
          ) : field.type === 'select' ? (
            <select
              name={field.name}
              value={formData[field.name] || ''}
              onChange={handleChange}
              className="w-full border rounded p-2"
              required={field.required}
            >
              <option value="">Select {field.label}</option>
              {field.options?.map(opt => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          ) : (
            <input
              type={field.type}
              name={field.name}
              value={formData[field.name] || ''}
              onChange={handleChange}
              className="w-full border rounded p-2"
              required={field.required}
            />
          )}
          {errors[field.name] && <span className="text-red-600 text-sm">{errors[field.name]}</span>}
        </div>
      ))}
      <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 w-full">
        {submitText}
      </button>
    </form>
  );
}
